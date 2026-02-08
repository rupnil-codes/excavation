# fixd by gemini
from textual.widgets import Label
from textual.containers import Container
from textual import events
from assets.music_manager import play_sfx

class DialogueBox(Container):
    # 🚨 CRITICAL FIX 1: Allow this box to accept input
    can_focus = True 

    def __init__(self, text_to_show, **kwargs):
        super().__init__(**kwargs)
        self.full_text = text_to_show
        self.current_text = ""
        self.char_index = 0
        self.is_typing = True
        
        # Wrapper Styles
        self.styles.layer = "overlay"
        self.styles.dock = "bottom"
        self.styles.width = "100%"
        self.styles.height = "auto"
        self.styles.align = ("center", "middle")
        self.styles.margin_bottom = 2 

    def compose(self):
        with Container(id="box-border"):
            yield Label("", id="text-label")

    def on_mount(self):
        # 🚨 CRITICAL FIX 2: Steal focus immediately so keys work
        self.focus()
        
        inner = self.query_one("#box-border")
        
        # Dynamic Width Calculation
        lines = self.full_text.split('\n')
        longest_line = max(len(line) for line in lines) if lines else 0
        final_width = longest_line + 6
        
        inner.styles.width = final_width
        inner.styles.max_width = "90%" 
        
        # Styling
        inner.styles.height = "auto"
        inner.styles.border = ("double", "white")
        inner.styles.background = "black"
        inner.styles.color = "white"
        inner.styles.text_align = "center"
        inner.styles.padding = (1, 2)
        
        self.set_interval(0.05, self.type_next_letter)

    def type_next_letter(self):
        if self.char_index < len(self.full_text):
            char = self.full_text[self.char_index]
            self.current_text += char
            self.query_one("#text-label").update(self.current_text)
            if char != " ":
                play_sfx("voice")
            self.char_index += 1
        else:
            self.is_typing = False

    def on_key(self, event: events.Key):
        # 🚨 CRITICAL FIX 3: Prevent the map from moving while we press Z
        event.stop() 

        if event.key == "enter" or event.key == "z":
            if self.is_typing:
                return
            else:
                # If done typing, close the box
                self.remove()

# old code
# from textual.widgets import Label
# from textual.containers import Container
# from textual import events
# from assets.music_manager import play_sfx

# class DialogueBox(Container): #no cscscs
#     def __init__(self, text_to_show, **kwargs):
#         super().__init__(**kwargs)
#         self.full_text = text_to_show
#         self.current_text = ""
#         self.char_index = 0
#         self.is_typing = True
#         #gwmini start
#         self.styles.layer = "overlay"
#         self.styles.dock = "bottom"
#         self.styles.width = "100%"
#         self.styles.height = "auto" # Allow height to shrink if needed
#         self.styles.align = ("center", "middle")
#         self.styles.margin_bottom = 2 
# # g end
#     def compose(self):
#         with Container(id="box-border"):
#             yield Label("", id="text-label")

#     def on_mount(self):
#         inner = self.query_one("#box-border")
        
#         lines = self.full_text.split('\n')
#         longest_line = max(len(line) for line in lines)
        
#         final_width = longest_line + 6
        
#         # g start
#         inner.styles.width = final_width
#         inner.styles.max_width = "90%" 
        
#         # Standard Styling
#         inner.styles.height = "auto"
#         inner.styles.border = ("double", "white")
#         inner.styles.background = "black"
#         inner.styles.color = "white"
#         inner.styles.text_align = "center"
#         inner.styles.padding = (1, 2)
#         # g end
#         self.set_interval(0.05, self.type_next_letter)

#     def type_next_letter(self):
#         if self.char_index < len(self.full_text):
#             char = self.full_text[self.char_index]
#             self.current_text += char
#             self.query_one("#text-label").update(self.current_text)
#             if char != " ":
#                 play_sfx("voice")
#             self.char_index += 1
#         else:
#             self.is_typing = False

#     def on_key(self, event: events.Key):
#         if event.key == "enter" or event.key == "z":
#             if self.is_typing:
#                 self.is_typing = False
#                 self.char_index = len(self.full_text)
#                 self.current_text = self.full_text
#                 self.query_one("#text-label").update(self.full_text)
#             else:
#                 self.remove()