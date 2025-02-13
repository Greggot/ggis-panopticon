from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

class PanopticonApp(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


def start_interactive() :
    app = PanopticonApp()
    app.run()