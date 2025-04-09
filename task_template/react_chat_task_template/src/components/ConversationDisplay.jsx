import { useState, useEffect, useRef } from 'react';
import ConversationItem from "./ConversationItem";
import taskService from '../services/task'

const ConversationDisplay = ({ topic, format, number, isLoading, setIsLoading, isDisabled, comments, addComment, references, setReferences, setFinalList, setIsFinished, isFinished }) => {
  const [newComment, setNewComment] = useState("");
  const commentsRef = useRef(null);

  useEffect(() => {
    if (commentsRef.current) {
      commentsRef.current.scrollTop = commentsRef.current.scrollHeight;
    }    
  }, [comments])

  const replaceReferences = (newReferences) => {
    const oldReferences = JSON.parse(JSON.stringify(references));
    const replacementReferences = oldReferences.map(reference => {
      const replacementReference = newReferences.find(newReference => newReference.number === reference.number);
      return replacementReference ? replacementReference : reference;
    });
    console.log(replacementReferences);
    setReferences(replacementReferences);
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!newComment.trim()) {
      return;
    }
    addComment({ sender: "user", comment: newComment });
    setIsLoading(true);
    console.log(comments);

    taskService
        .submitUserInput({
          inputData: {
            comment: newComment,
          },
          objective: `Topic: ${topic}, citation format: ${format}, number of references: ${number}`
        })
        .then((returnedResponse) => {
          let parsed = taskService.parseAIResponse(returnedResponse.text)
          console.log(returnedResponse.text);
          const referencesBlock = parsed.references;
          const commentBlock = parsed.comment;
          if (referencesBlock) {
            if (taskService.checkForJSON(referencesBlock)) {
              let newReferences = JSON.parse(referencesBlock);
              replaceReferences(newReferences);
            } else {
              console.log(referencesBlock);
              console.log(JSON.parse(referencesBlock));
              setFinalList(JSON.parse(referencesBlock));
              setIsFinished(true);
            }
          }
          if (commentBlock) {
            addComment({ sender: "ai", comment: commentBlock });
          }
          setIsLoading(false)
        })
        .catch((error) => {
          console.log(error)
        });
    setNewComment("");
  };

  return (
    <div className="chat-space-wrapper">
      <h2>Conversation</h2>
      <div className="chat-space">
        <div className="messages" ref={commentsRef}>
          {comments
            .map((comment, index) => (
              <ConversationItem key={index} comment={comment} /> 
            ))
          }
        </div>
        {isLoading && <div className="loading-text">Waiting for AI response...</div>} 
        <div className="form-wrapper">
          <form onSubmit={handleSubmit} className="input-form">
            <input 
              value={newComment}
              disabled={!isDisabled || isLoading || isFinished}
              onChange={(event) => setNewComment(event.target.value)} 
              placeholder="Send a message to the AI" 
            />
            <button type="submit" 
              disabled={!isDisabled || isLoading || isFinished}
              onClick={handleSubmit}> 
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ConversationDisplay;
