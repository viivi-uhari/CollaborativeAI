const DialogueItem = ({ message, style }) => {
  const messageClass = message.sender === "user" ? "user-dialogue" : "ai-dialogue";

  const parsedJSON = JSON.parse(message.text)

  return (
    <>
      
    </>
  );
};

export default DialogueItem;
