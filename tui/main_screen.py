from textual import events, on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TextArea, Button, ProgressBar
from textual.containers import HorizontalGroup, VerticalScroll

from utils.card_creator_config import Card_creator_config
from kaiten.session_manager import get_session
from tasks_parser.simple import create_cards_from_text_file_bugs, create_cards_from_text_file_features

class ControlPanel(HorizontalGroup) :
    # def on_button_pressed(self, event: Button.Pressed) -> None:
    #     """Event handler called when a button is pressed."""
    #     if event.button.id == "create":
    #         self.add_class("created")

    def compose(self) -> ComposeResult:
        """Create child widgets of a stopwatch."""
        yield Button("Create cards", id="create", variant="success")

class PanopticonApp(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "tcss/main.tcss"

    def __init__(self, task_path):
        super(PanopticonApp, self).__init__()
        
        self.task_path = task_path

        with open(task_path) as task_file:
            self.content = task_file.read()

    def compose(self) -> ComposeResult:
        self.header = Header()
        self.textarea = TextArea(text = self.content)
        self.control_panel = ControlPanel()
        self.footer = Footer()
        yield self.header
        yield self.textarea
        yield self.control_panel
        yield self.footer

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = ("textual-dark" if self.theme == "textual-light" else "textual-light")

    @on(Button.Pressed, "#create")
    def pressed_create(self) -> None:
        """Pressed Create"""
        content = self.textarea.text

        with open(self.task_path, "w") as file:
            file.write(content)
        
        config_name = 'delivery'
        (user, session) = get_session('env/env.json')
        config = Card_creator_config(config_name, user)
        # create_cards_from_text_file_bugs('data/tasks.txt', config)
        create_cards_from_text_file_features(session=session, path='data/tasks.txt', config=config)
        exit(0)

def start_interactive(task_file) :
    app = PanopticonApp(task_file)
    app.run()

if __name__ == "__main__":
    start_interactive("data/tasks.txt")