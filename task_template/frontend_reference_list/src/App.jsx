import { useState, useRef, useEffect } from 'react';
import Header from "./components/Header";
import Footer from "./components/Footer";
import Feedback from "./components/Feedback";
import Dialogue from "./components/Dialogue";
import ConversationDisplay from "./components/ConversationDisplay";
import TaskDescription from './components/TaskDescription';
import VisualWarning from './components/VisualWarning';
import TopicSummary from './components/TopicSummary';
import TopicForm from './components/TopicForm';
import React from 'react';
import { topics } from "./utils/config";
import "./index.css";
import IdModal from './components/IdModal';

const App = () => {
  const [isFinished, setIsFinished] = useState(false);
  const viewPointRef = useRef(null);

  const [topic, setTopic] = useState(topics[0]);
  const [format, setFormat] = useState("");
  const [number, setNumber] = useState(1);
  const [isDisabled, setIsDisabled] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const [references, setReferences] = useState([]);
  const [comments, setComments] = useState([]);
  const [finalList, setFinalList] = useState([]);

  const [currentWarning, setWarning] = useState(null);
  const [warningModalIsOpen, setWarningIsOpen] = useState(false);
  const [idModalIsOpen, setIdIsOpen] = useState(true);
  const [participantId, setId] = useState(null);

  const [elapsedTime, setElapsedTime] = useState(0);
  const timerRef = useRef(null);

  function closeIdModal() {
    setIdIsOpen(false);
  }
  function openIdModal() {
    setIdIsOpen(true);
  }
  function closeWarningModal() {
    setWarningIsOpen(false);
  }
  function openWarningModal() {
    setWarningIsOpen(true);
  }
  
  useEffect(() => {
    if (isFinished) {
      if (viewPointRef.current) {
        viewPointRef.current.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }
  }, [isFinished]);

  useEffect(() => {
    timerRef.current = setInterval(() => {
      setElapsedTime(prev => prev + 1);
    }, 1000);

    return () => clearInterval(timerRef.current);
  }, []);

  useEffect(() => {
    if (isFinished && timerRef.current) {
      clearInterval(timerRef.current);
      console.log("Timer stopped at:", elapsedTime, "seconds");
    }
  }, [isFinished]);

  const addComment = (comment) => {
    setComments(previousComments => previousComments.concat(comment));
  };

  return (
    <>
      <Header />
      <IdModal participantId={participantId} setId={setId} idModalIsOpen={idModalIsOpen} closeIdModal={closeIdModal}/>
      <TaskDescription/>
      {!isDisabled && <TopicForm 
        topic={topic} setTopic={setTopic} 
        format={format} setFormat={setFormat} 
        number={number} setNumber={setNumber} 
        isDisabled={isDisabled} 
        setIsDisabled={setIsDisabled} 
        setIsLoading={setIsLoading}
        setReferences={setReferences}
        addComment={addComment}
        openWarningModal={openWarningModal}
      />}
      {isDisabled && <TopicSummary topic={topic} format={format} number={number}/>}
      {participantId && <VisualWarning
        participantId={participantId}
        warningModalIsOpen={warningModalIsOpen}
        closeWarningModal={closeWarningModal}
        currentWarning={currentWarning}
        setWarning={setWarning}
      />}
      <div className="main-interaction">
        <Dialogue isLoading={isLoading} setIsLoading={setIsLoading} references={references} finalList={finalList}/>
        <ConversationDisplay
          topic={topic}
          format={format}
          number={number}
          isDisabled={isDisabled} 
          setIsDisabled={setIsDisabled} 
          isLoading={isLoading} 
          setIsLoading={setIsLoading}
          comments={comments}
          references={references}
          setReferences={setReferences}
          addComment={addComment}
          setFinalList={setFinalList}
          setIsFinished={setIsFinished}
          isFinished={isFinished}
        />
      </div>
      <div className='bottom-container'>
        <div className='bottom-filler'></div>
        {isFinished ? <Feedback elapsedTime={elapsedTime}/> : <div className='feedback-filler'></div>}
        {(participantId % 3 == 1) ? 
          <button type='button' className='modal-warning-btn' onClick={openWarningModal}>
            <svg width="30" height="32" viewBox="0 0 30 32" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M13.2411 6.24957C13.9974 4.85226 16.0026 4.85226 16.7589 6.24957L26.3926 24.048C27.1138 25.3806 26.1489 27 24.6337 27H5.36632C3.85106 27 2.88616 25.3806 3.60745 24.048L13.2411 6.24957Z" fill="#FFA100"/>
              <path d="M16.2551 13.1818L16.0682 20.0565H14.3136L14.1218 13.1818H16.2551ZM15.1909 23.1246C14.8745 23.1246 14.6028 23.0128 14.3759 22.7891C14.149 22.5621 14.0371 22.2905 14.0403 21.9741C14.0371 21.6609 14.149 21.3924 14.3759 21.1687C14.6028 20.945 14.8745 20.8331 15.1909 20.8331C15.4945 20.8331 15.7614 20.945 15.9915 21.1687C16.2216 21.3924 16.3382 21.6609 16.3414 21.9741C16.3382 22.185 16.2823 22.3784 16.1737 22.5542C16.0682 22.7267 15.9292 22.8658 15.7566 22.9712C15.584 23.0735 15.3954 23.1246 15.1909 23.1246Z" fill="white"/>
            </svg>
          </button>
        : <div className='bottom-filler'></div>}
      </div>
      <Footer/>
    </>
  );
};

export default App;
