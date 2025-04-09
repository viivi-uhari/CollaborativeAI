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
import constants from './constants/constants';
import "./index.css";

const App = () => {
  const [isFinished, setIsFinished] = useState(false);
  const [isRatingSubmitted, setIsRatingSubmitted] = useState(false);
  const viewPointRef = useRef(null);

  const [topic, setTopic] = useState(constants.topics[0]);
  const [format, setFormat] = useState("");
  const [number, setNumber] = useState(1);
  const [isDisabled, setIsDisabled] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const [references, setReferences] = useState([]);
  const [comments, setComments] = useState([]);
  const [finalList, setFinalList] = useState([]);

  const [currentWarning, setWarning] = useState(null);
  const [modalIsOpen, setIsOpen] = React.useState(true);

  const [elapsedTime, setElapsedTime] = useState(0);
  const timerRef = useRef(null);

  function closeModal() {
    setIsOpen(false);
  }
  
  useEffect(() => {
    if (isFinished) {
      if (viewPointRef.current) {
        viewPointRef.current.scrollIntoView({ behavior: "smooth", block: "center"});
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
      />}
      {isDisabled && <TopicSummary topic={topic} format={format} number={number}/>}
       <VisualWarning
        modalIsOpen={modalIsOpen}
        closeModal={closeModal}
        currentWarning={currentWarning}
        setWarning={setWarning}/>
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
      {isFinished && <Feedback elapsedTime={elapsedTime}/>}
      <Footer />
    </>
  );
};

export default App;
