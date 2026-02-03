# Acme modules
from acme.utils import formatting as fmt


class TestFormatting:
    """Test the formatting module."""

    def test_colorize(self):
        """Test colorize."""
        out_string = fmt.colorize('message', 'green')
        assert out_string == '[green]message[/green]'
