# from dotenv import dotenv_values
# from PyQt5.QtWidgets import (
#     QApplication,
#     QWidget,
#     QVBoxLayout,
#     QHBoxLayout,
#     QLineEdit,
#     QPushButton,
#     QLabel,
#     QListWidget,
#     QListWidgetItem,
# )
# from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap
# from PyQt5.QtCore import Qt, QSize
# import sys
# from health_advisor import ChatBot
# from datetime import datetime

# # Load Assistant name from .env
# env_vars = dotenv_values(".env")

# Assistantname = env_vars.get("Assistantname", "HealthBot")  # Default if null

# class ChatBubble(QWidget):
#     def __init__(self, message, is_user=False, timestamp=""):
#         super().__init__()
#         layout = QHBoxLayout()
#         layout.setContentsMargins(10, 5, 10, 5)
#         layout.setSpacing(5)

#         # Message container
#         message_container = QVBoxLayout()
#         message_container.setSpacing(2)

#         # Message label
#         message_label = QLabel(message)
#         message_label.setWordWrap(True)
#         message_label.setFont(QFont("Segoe UI", 11))
        
#         # Dynamically adjust width based on message content
#         font_metrics = message_label.fontMetrics()
#         text_width = font_metrics.boundingRect(message).width()
#         max_bubble_width = 400  # Max width limit (e.g., 70% of chat window)
#         min_bubble_width = 150  # Minimum width for consistency
        
#         # Set width dynamically, but cap at max_bubble_width
#         if text_width < max_bubble_width:
#             message_label.setFixedWidth(min(max_bubble_width, text_width + 24))  # +24 for padding
#         else:
#             message_label.setFixedWidth(max_bubble_width)

#         # Styling based on user or AI
#         if is_user:
#             message_label.setStyleSheet("""
#                 background-color: #25D366;
#                 color: white;
#                 padding: 8px 12px;
#                 border-radius: 10px;
#                 border-bottom-right-radius: 2px;
#                 box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
#             """)
#             time_label = QLabel(timestamp)
#             time_label.setFont(QFont("Segoe UI", 8))
#             time_label.setStyleSheet("color: #999999;")
#             time_label.setAlignment(Qt.AlignRight)
#             message_container.addWidget(message_label)
#             message_container.addWidget(time_label)
#             layout.addStretch()
#             layout.addLayout(message_container)
#         else:
#             message_label.setStyleSheet("""
#                 background-color: #FFFFFF;
#                 color: #333333;
#                 padding: 8px 12px;
#                 border-radius: 10px;
#                 border-bottom-left-radius: 2px;
#                 box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
#             """)
#             time_label = QLabel(timestamp)
#             time_label.setFont(QFont("Segoe UI", 8))
#             time_label.setStyleSheet("color: #999999;")
#             time_label.setAlignment(Qt.AlignLeft)
#             layout.addLayout(message_container)
#             message_container.addWidget(message_label)
#             message_container.addWidget(time_label)
#             layout.addStretch()

#         self.setLayout(layout)

#     def sizeHint(self):
#         return QSize(0, super().sizeHint().height() + 15)

# class HealthAdvisorUI(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Health Advisor AI")
#         self.setGeometry(200, 100, 700, 600)  # Slightly smaller for better fit
#         self.setWindowIcon(QIcon('Health_icon.png'))  # Replace with actual icon path
#         self.setStyleSheet("""
#             background: qlineargradient(
#                 x1: 0, y1: 0, x2: 1, y2: 1,
#                 stop: 0 #2E2E2E,
#                 stop: 0.5 #4A4A4A,
#                 stop: 1 #ECE5DD
#             );
#             color: #333333;
#             border-radius: 8px;
#         """)

#         # Main layout
#         layout = QVBoxLayout()
#         layout.setContentsMargins(10, 10, 10, 10)
#         layout.setSpacing(10)

#         # Title container with icon and text
#         title_container = QHBoxLayout()
#         title_container.setSpacing(8)

#         # Icon for title
#         title_icon = QLabel()
#         pixmap = QPixmap('chatbot.png')  # Replace with actual icon path
#         scaled_pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Scale to 32x32
#         title_icon.setPixmap(scaled_pixmap)
#         title_icon.setAlignment(Qt.AlignCenter)
#         title_container.addWidget(title_icon)

#         # Title text
#         self.title = QLabel("AI Health Assistant")
#         self.title.setFont(QFont("Segoe UI", 18, QFont.Bold))
#         self.title.setStyleSheet("""
#             color: #075E54;
#             padding: 10px;
#         """)
#         self.title.setAlignment(Qt.AlignCenter)
#         title_container.addWidget(self.title)

#         # Title background
#         title_widget = QWidget()
#         title_widget.setLayout(title_container)
#         title_widget.setStyleSheet("""
#             background-color: #128C7E;
#             border-radius: 8px;
#             padding: 10px;
#         """)
#         # Ensure title_widget doesn't stretch unnecessarily
#         # title_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
#         layout.addWidget(title_widget, alignment=Qt.AlignCenter)

#         #; # Chat area
#         self.chat_container = QListWidget()
#         self.chat_container.setStyleSheet("""
#             background-color: #ECE5DD;
#             border: none;
#             border-radius: 8px;
#             padding: 10px;
#             font-family: 'Segoe UI';
#             color: #333333;
#         """)
#         self.chat_container.setWordWrap(True)
#         self.chat_container.setSpacing(6)
#         self.chat_container.setContentsMargins(5, 5, 5, 5)
#         layout.addWidget(self.chat_container)

#         # Input field and send button layout
#         input_layout = QHBoxLayout()
#         input_layout.setSpacing(8)
#         input_layout.setContentsMargins(5, 5, 5, 5)

#         # Input field
#         self.input_field = QLineEdit()
#         self.input_field.setPlaceholderText("Type your health query...")
#         self.input_field.setStyleSheet("""
#             background-color: #FFFFFF;
#             color: #333333;
#             border: 1px solid #CCCCCC;
#             border-radius: 20px;
#             padding: 8px 12px;
#             font-size: 13px;
#         """)
#         self.input_field.setFixedHeight(40)  # Fixed height for compact look
#         self.input_field.returnPressed.connect(self.send_message)
#         input_layout.addWidget(self.input_field)

#         # Send button
#         self.send_button = QPushButton("Send")
#         self.send_button.setIcon(QIcon('send_icon.png'))  # Replace with actual send icon path
#         self.send_button.setIconSize(QSize(20, 20))  # Adjust icon size
#         self.send_button.setStyleSheet("""
#             QPushButton {
#                 background-color: #25D366;
#                 color: white;
#                 font-size: 13px;
#                 font-weight: bold;
#                 padding: 8px 15px;
#                 border-radius: 20px;
#                 border: none;
#                 text-align: center;
#             }
#             QPushButton:hover {
#                 background-color: #20BF55;
#             }
#             QPushButton:pressed {
#                 background-color: #1BAF4B;
#             }
#         """)
#         self.send_button.setFixedWidth(100)  # Slightly wider to fit icon and text
#         self.send_button.clicked.connect(self.send_message)
#         input_layout.addWidget(self.send_button)

#         layout.addLayout(input_layout)
#         self.setLayout(layout)

#     def send_message(self):
#         user_input = self.input_field.text().strip()
#         if user_input:
#             timestamp = datetime.now().strftime("%I:%M %p")
#             self.append_message(f"{user_input}", is_user=True, timestamp=timestamp)
#             self.input_field.clear()
#             response = ChatBot(user_input)
#             self.append_message(f"{response}", is_user=False, timestamp=timestamp)

#     def append_message(self, message, is_user=False, timestamp=""):
#         bubble = ChatBubble(message, is_user, timestamp)
#         item = QListWidgetItem(self.chat_container)
#         item.setSizeHint(bubble.sizeHint())
#         self.chat_container.addItem(item)
#         self.chat_container.setItemWidget(item, bubble)
#         self.chat_container.scrollToBottom()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setStyle("Fusion")
#     window = HealthAdvisorUI()
#     window.show()
#     sys.exit(app.exec_())








from dotenv import dotenv_values
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QListWidget,
    QListWidgetItem,
)
from PyQt5.QtGui import QFont, QColor, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, QEvent
import sys
from health_advisor import ChatBot
from datetime import datetime

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname", "HealthBot")

class ChatBubble(QWidget):
    def __init__(self, message, is_user=False, timestamp=""):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)
        message_container = QVBoxLayout()
        message_container.setSpacing(2)
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setFont(QFont("Segoe UI", 11))
        font_metrics = message_label.fontMetrics()
        text_width = font_metrics.boundingRect(message).width()
        max_bubble_width = 400
        min_bubble_width = 150
        if text_width < max_bubble_width:
            message_label.setFixedWidth(min(max_bubble_width, text_width + 24))
        else:
            message_label.setFixedWidth(max_bubble_width)
        if is_user:
            message_label.setStyleSheet("""
                background-color: #25D366;
                color: white;
                padding: 8px 12px;
                border-radius: 10px;
                border-bottom-right-radius: 2px;
                box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
            """)
            time_label = QLabel(timestamp)
            time_label.setFont(QFont("Segoe UI", 8))
            time_label.setStyleSheet("color: #999999;")
            time_label.setAlignment(Qt.AlignRight)
            message_container.addWidget(message_label)
            message_container.addWidget(time_label)
            layout.addStretch()
            layout.addLayout(message_container)
        else:
            message_label.setStyleSheet("""
                background-color: #FFFFFF;
                color: #333333;
                padding: 8px 12px;
                border-radius: 10px;
                border-bottom-left-radius: 2px;
                box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
            """)
            time_label = QLabel(timestamp)
            time_label.setFont(QFont("Segoe UI", 8))
            time_label.setStyleSheet("color: #999999;")
            time_label.setAlignment(Qt.AlignLeft)
            layout.addLayout(message_container)
            message_container.addWidget(message_label)
            message_container.addWidget(time_label)
            layout.addStretch()
        self.setLayout(layout)

    def sizeHint(self):
        return QSize(0, super().sizeHint().height() + 15)

class HealthAdvisorUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Health Advisor AI")
        self.setGeometry(200, 100, 700, 600)
        self.setWindowIcon(QIcon('Health_icon.png'))
        self.setStyleSheet("""
            background: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #2E2E2E,
                stop: 0.5 #4A4A4A,
                stop: 1 #ECE5DD
            );
            color: #333333;
            border-radius: 8px;
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        title_container = QHBoxLayout()
        title_container.setSpacing(8)
        title_icon = QLabel()
        pixmap = QPixmap('chatbot.png')
        scaled_pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        title_icon.setPixmap(scaled_pixmap)
        title_icon.setAlignment(Qt.AlignCenter)
        title_container.addWidget(title_icon)
        self.title = QLabel("AI Health Assistant")
        self.title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.title.setStyleSheet("""
            color: #075E54;
            padding: 10px;
        """)
        self.title.setAlignment(Qt.AlignCenter)
        title_container.addWidget(self.title)
        title_widget = QWidget()
        title_widget.setLayout(title_container)
        title_widget.setStyleSheet("""
            background-color: #128C7E;
            border-radius: 8px;
            padding: 10px;
        """)
        layout.addWidget(title_widget, alignment=Qt.AlignCenter)
        self.chat_container = QListWidget()
        self.chat_container.setStyleSheet("""
            background-color: #ECE5DD;
            border: none;
            border-radius: 8px;
            padding: 10px;
            font-family: 'Segoe UI';
            color: #333333;
        """)
        self.chat_container.setWordWrap(True)
        self.chat_container.setSpacing(6)
        self.chat_container.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.chat_container)
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)
        input_layout.setContentsMargins(5, 5, 5, 5)
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your health query...")
        self.input_field.setStyleSheet("""
            background-color: #FFFFFF;
            color: #333333;
            border: 1px solid #CCCCCC;
            border-radius: 20px;
            padding: 8px 12px;
            font-size: 13px;
        """)
        self.input_field.setFixedHeight(40)
        self.input_field.returnPressed.connect(self.send_message)
        self.input_field.installEventFilter(self)
        input_layout.addWidget(self.input_field)
        self.send_button = QPushButton("Send")
        self.send_button.setIcon(QIcon('send_icon.png'))
        self.send_button.setIconSize(QSize(20, 20))
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #25D366;
                color: white;
                font-size: 13px;
                font-weight: bold;
                padding: 8px 15px;
                border-radius: 20px;
                border: none;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #20BF55;
            }
            QPushButton:pressed {
                background-color: #1BAF4B;
            }
        """)
        self.send_button.setFixedWidth(100)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)
        self.setLayout(layout)
        self.input_field.setFocus()

    def eventFilter(self, obj, event):
        if obj == self.input_field and event.type() == QEvent.KeyPress:
            if (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter) and event.modifiers() & Qt.ControlModifier:
                self.send_message()
                return True
        return super().eventFilter(obj, event)

    def send_message(self):
        user_input = self.input_field.text().strip()
        if user_input:
            timestamp = datetime.now().strftime("%I:%M %p")
            self.append_message(f"{user_input}", is_user=True, timestamp=timestamp)
            self.input_field.clear()
            self.input_field.setFocus()
            loading_item = self.append_message(f"{Assistantname} is typing...", is_user=False, timestamp=timestamp, is_loading=True)
            try:
                response = ChatBot(user_input)
                self.remove_loading_message(loading_item)
                self.append_message(f"{response}", is_user=False, timestamp=datetime.now().strftime("%I:%M %p"))
            except Exception as e:
                self.remove_loading_message(loading_item)
                error_msg = (
                    "Sorry, I couldn't process your request right now. "
                    "Please check your internet connection and try again."
                )
                self.append_message(error_msg, is_user=False, timestamp=datetime.now().strftime("%I:%M %p"))

    def append_message(self, message, is_user=False, timestamp="", is_loading=False):
        bubble = ChatBubble(message, is_user, timestamp)
        item = QListWidgetItem(self.chat_container)
        item.setSizeHint(bubble.sizeHint())
        self.chat_container.addItem(item)
        self.chat_container.setItemWidget(item, bubble)
        self.chat_container.scrollToBottom()
        if is_loading:
            return item
        return None

    def remove_loading_message(self, item):
        if item is not None:
            row = self.chat_container.row(item)
            self.chat_container.takeItem(row)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = HealthAdvisorUI()
    window.show()
    sys.exit(app.exec_())
