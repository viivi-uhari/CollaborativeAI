import { useState, useEffect, useRef } from 'react';
import DialogueItem from "./DialogueItem";
import { dialogueType } from "../utils/config";
import { lengthLimit } from '../utils/config';

const Dialogue = ({ isDisabled, messages, setMessages, addMessage }) => {
  const [newLine, setNewLine] = useState("");
  const [newComment, setNewComment] = useState("");
  const [isLengthReached, setIsLengthReached] = useState(false);
  const messagesRef = useRef(null);

  useEffect(() => {
    setIsLengthReached(messages.filter(msg => msg.text !== "" && msg.text !== null).length === lengthLimit)
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }    
  }, [messages])

  let style = "none";
  if (dialogueType === "paragraph") {
    style = "dialogue-paragraph";
  } else {
    style = "dialogue-poem";
  }

  const handleEditMessage = (index, newMessage) => {
    if (!newMessage.trim()) {
      alert("Please save a non empty dialogue");
    } else {
      setMessages(messages.map((message, idx) => idx !== index ? message : { ...message, text: newMessage }))
    }
  };

  function parsePoetryAndComment(input) {
    // Initialize variables to store the parsed parts
    let poetryLine = "";
    let comment = "";

    // Trim the input to remove leading/trailing whitespace
    input = input.trim();

    // Check if the input starts with a '[' character
    if (input.startsWith('[')) {
        // Find the closing ']' character
        let endBracketIndex = input.indexOf(']');
        
        // If a closing ']' is found, extract the poetry line
        if (endBracketIndex !== -1) {
            poetryLine = input.substring(1, endBracketIndex).trim();
            // Extract the comment part if there is any text after the closing ']'
            if (endBracketIndex + 1 < input.length) {
                comment = input.substring(endBracketIndex + 1).trim();
            }
        }
    } else {
        // If the input doesn't start with '[', consider the whole input as a comment
        comment = input;
    }

    console.log("Parsed: ", poetryLine, ", ", comment)

    return { poetryLine, comment };
  }

  function checkAndAddMessage(sender, text, comment, type) {
    text = (typeof text === 'string' && text.trim()) ? text : null;
    comment = (typeof comment === 'string' && comment.trim()) ? comment : null;

    if (text === null && comment === null) {
      console.log("no message");
    } else {
      addMessage({ sender: sender, text: text, comment: comment, type: "dialogue"}); 
    }
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    
    checkAndAddMessage("user", newLine, newComment,"dialogue");   

    if (isLengthReached) {
      newComment += " The poem is finished. Do NOT add a new poetry line.";
    }

    taskService
        .submitUserInput({inputData: { commentData: newComment}, text: newLine, ojective: theme})
        .then((returnedResponse) => {
          let parsed = parsePoetryAndComment(returnedResponse.text)
          checkAndAddMessage("ai", parsed.poetryLine, parsed.comment,"dialogue")
        })
        .catch((error) => {
          console.log(error)
        });
        setNewLine("");
        setNewComment("");
  };

  return (
    <div className="dialogue-wrapper">
      <h2>Your joint poem</h2>
      <div className="dialogue">
        <div className="dialogue-content" ref={messagesRef}>
          {messages
            .map((msg, idx) => ({ ...msg, originalIndex: idx })) // Preserve original index
            .filter(msg => msg.text !== "" && msg.text !== null)
            .map((msg) => (
              <DialogueItem
                key={msg.originalIndex} // Use original index as key if needed
                idx={msg.originalIndex} // Pass original index as `idx`
                message={msg}
                handleEditMessage={handleEditMessage}
                style={style}
              />
            ))}
        </div>
        <div className="form-wrapper">
          <form onSubmit={handleSubmit}>
            <div className="input-form">  
              <textarea 
                value={newLine}
                disabled={isLengthReached || !isDisabled}
                className={isLengthReached ? "disabled" : ""}
                onChange={(event) => setNewLine(event.target.value)}
                placeholder="Add a line to the poem" 
              />
            </div>
          </form>
          <div className="submit-button">
              <button type="submit" 
                style={{
                  backgroundColor: "#4caf50"
                }}
                disabled={isLengthReached || !isDisabled}
                className={isLengthReached ? "disabled" : ""}
                onClick={handleSubmit}> 
                Add new line
              </button>
          </div>
      </div>
      </div>
    </div>
  );
};

export default Dialogue;
