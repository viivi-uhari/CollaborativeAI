const DialogueItem = ({ message, style }) => {
  const messageClass = message.sender === "user" ? "user-dialogue" : "ai-dialogue";

  return (
    <>
      <div className={`dialogue-poem ${messageClass}`}>
          {message.text} <br/> 
      </div>
    </>
  );
};

export default DialogueItem;
