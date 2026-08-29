// © 2026 aiaiaiai · aiaiaiai.org

use std::{fmt, str::FromStr};

use thiserror::Error;

const PREFIX: &str = "0x";
const MIN_SLUG_SCALARS: usize = 2;
const MAX_SLUG_SCALARS: usize = 32;

#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct PubDress(String);

impl PubDress {
    #[must_use]
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl fmt::Display for PubDress {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(&self.0)
    }
}

impl FromStr for PubDress {
    type Err = PubDressError;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        let slug = value
            .strip_prefix(PREFIX)
            .ok_or(PubDressError::InvalidPrefix)?;
        let scalar_count = slug.chars().count();

        if !(MIN_SLUG_SCALARS..=MAX_SLUG_SCALARS).contains(&scalar_count) {
            return Err(PubDressError::InvalidLength);
        }

        if !slug.chars().all(is_allowed_slug_scalar) {
            return Err(PubDressError::InvalidCharacter);
        }

        Ok(Self(value.to_owned()))
    }
}

fn is_allowed_slug_scalar(value: char) -> bool {
    value.is_ascii_lowercase()
        || value.is_ascii_digit()
        || matches!(
            value,
            '-' | '/'
                | ':'
                | ';'
                | '('
                | ')'
                | '₴'
                | '&'
                | '@'
                | '"'
                | '.'
                | ','
                | '?'
                | '!'
                | '\''
                | '['
                | ']'
                | '{'
                | '}'
                | '#'
                | '%'
                | '^'
                | '*'
                | '+'
                | '='
                | '_'
                | '\\'
                | '|'
                | '~'
                | '<'
                | '>'
                | '€'
                | '$'
                | '£'
                | '•'
        )
}

#[derive(Clone, Copy, Debug, Eq, Error, PartialEq)]
pub enum PubDressError {
    #[error("pub_dress must start with the literal 0x prefix")]
    InvalidPrefix,
    #[error("pub_dress slug must contain 2 to 32 Unicode scalar values")]
    InvalidLength,
    #[error("pub_dress contains a scalar outside the canonical allowlist")]
    InvalidCharacter,
}

#[cfg(test)]
mod tests {
    use std::str::FromStr;

    use super::{PubDress, PubDressError};

    #[test]
    fn accepts_canonical_handles_without_rewriting_them() {
        let values = [
            "0x0sky",
            "0xab",
            "0xa/b?c#d%20",
            "0x₴€$£•",
            "0x-/:;()&@\".,?!'[]{}#%^*+=_\\|~<>",
        ];

        for value in values {
            let parsed = PubDress::from_str(value).expect("canonical pub_dress must parse");
            assert_eq!(parsed.as_str(), value);
        }
    }

    #[test]
    fn rejects_noncanonical_prefix_and_length() {
        assert_eq!(
            PubDress::from_str("1xsky"),
            Err(PubDressError::InvalidPrefix)
        );
        assert_eq!(PubDress::from_str("0xa"), Err(PubDressError::InvalidLength));
        assert_eq!(
            PubDress::from_str(&format!("0x{}", "a".repeat(33))),
            Err(PubDressError::InvalidLength)
        );
    }

    #[test]
    fn rejects_values_that_would_require_normalization() {
        for value in [
            "0xSky",
            "0xпривіт",
            "0xa b",
            "0xa🙂",
            "0xa\u{0301}",
            "0x‘a",
            " 0xsky",
            "0xsky ",
        ] {
            assert!(PubDress::from_str(value).is_err(), "accepted {value:?}");
        }
    }
}
