const DialogueItem = ({ reference }) => {
  const messageClass = reference.sender === "user" ? "user-dialogue" : "ai-dialogue";

  return (
    <>
      <div className={`dialogue-poem ${messageClass}`}>
          <div className="reference-item">
            <p className="reference-detail" id="reference-title"><b>{reference.number}. {reference.title}</b></p>
            <p className="reference-detail">{reference.citation}</p>
            <p className="reference-detail" id="reference-summary"><b>Summary:</b>{reference.summary}</p> 
            <div className="reference-metadata">
              <p className="reference-detail"><strong>{"Published in: "}</strong>{reference.publisher}</p>
              <p className="reference-detail"><strong>{"Link: "}</strong><a href={reference.link} target="_blank">{reference.link}</a></p> 
            </div>
          </div>
      </div>
    </>
  );
};

export default DialogueItem;
