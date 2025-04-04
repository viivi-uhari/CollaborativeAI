import { useEffect, useRef } from 'react';
import DialogueItem from "./DialogueItem";

const Dialogue = ({ isLoading, references }) => {
  const referencesRef = useRef(null);

  console.log(references);

  useEffect(() => {
    if (referencesRef.current) {
      referencesRef.current.scrollTop = referencesRef.current.scrollHeight;
    }    
  }, [references])

  return (
    <div className="dialogue-wrapper">
      <h2>References</h2>
      <div className="dialogue">
        <div className="dialogue-content" ref={referencesRef}>
        {references
          .map((reference, index) => (
            <DialogueItem key={index} reference={reference}/>
        ))}
        </div>
        {isLoading && <div className="loading-text">Waiting for AI response...</div>} 
      </div>
    </div>
  );
};

export default Dialogue;
