import { useEffect, useRef } from 'react';
import DialogueItem from "./DialogueItem";
import FinalList from './FinalList';

const Dialogue = ({ isLoading, references, finalList }) => {
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
        {finalList.length > 0 ?
          <FinalList finalList={finalList}/>
          : references.map((reference, index) => (
            <DialogueItem key={index} reference={reference}/>
        ))}
        </div>
        {isLoading && <div className="loading-text">Waiting for AI response...</div>} 
      </div>
    </div>
  );
};

export default Dialogue;
