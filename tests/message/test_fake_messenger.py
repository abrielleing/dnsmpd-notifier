from message.fake_messenger import FakeMessenger

def test_send():
    msg = FakeMessenger()

    assert msg.sender == None

    msg.send('John Smith', 'Jane Doe', 'Hello', 'Hello World', '<p>Hello World</p>')

    assert msg.sender == 'John Smith'
    assert msg.recipient == 'Jane Doe'
    assert msg.subject == 'Hello'
    assert msg.message_text == 'Hello World'
    assert msg.message_html == '<p>Hello World</p>'
