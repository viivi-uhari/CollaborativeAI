import taskService from "../services/task"

const topicForm = ({ topic, setTopic, format, setFormat, number, setNumber, isDisabled, setIsDisabled, setIsLoading }) => {
  
  const chooseTopic = (event) => {
    if (!topic.trim()) {
      alert("Please enter a topic");
      return;
    }
    event.preventDefault();
    setIsDisabled(true);
    setIsLoading(true);
  };

  return (
    <>
      <div className="topic-wrapper">
        <form onSubmit={chooseTopic} className="topic-input">
          <label for="topic"><h3>Topic</h3></label>
          <input 
            id="topic"
            name="topic"
            type="text" 
            disabled={isDisabled}
            placeholder="Define a topic for the references"
            value={topic}
            onChange={(event) => setTopic(event.target.value)}
          />
          <label for="format"><h3>Citation format</h3></label>
          <input 
            id="format"
            name="format"
            type="text" 
            disabled={isDisabled}
            placeholder="Define the citatin format format the references"
            value={format}
            onChange={(event) => setFormat(event.target.value)}
          />
          <label for="number"><h3>Number of references</h3></label>
          <input 
            id="number"
            name="number"
            type="number"
            min="1" 
            max="50" 
            disabled={isDisabled}
            placeholder="Set the number of references"
            value={number}
            onChange={(event) => setNumber(event.target.value)}
          />
          <button 
            type="button"
            disabled={isDisabled}
            className="topic-submit-btn"
            onClick={chooseTopic}>
            Submit 
          </button>
        </form>
      </div>
    </>
  );
};

export default topicForm;
