const ConversationalItem = ({ comment }) => {
  const commentClass = comment.sender === "user" ? "user-message" : "ai-message";
  const avatarClass = comment.sender === "user" ? "avatar-user" : "avatar-ai";
  const avatarText = comment.sender === "user" ? "You" : "AI";

  return (
    <>
      <div className={`message ${commentClass}`}>
        {comment.sender === "user" ? (
          <>
            {comment.comment}
            <div className={`avatar ${avatarClass}`}> {avatarText} </div>
          </>
        ) : (
          <>
            <div className={`avatar ${avatarClass}`}> {avatarText} </div>
            {comment.comment}
          </>
        )}
      </div>
    </>
    
  );
};

export default ConversationalItem;
