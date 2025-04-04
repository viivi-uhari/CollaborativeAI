import taskService from "../services/task"
import constants from "../constants/constants";

const TopicForm = ({ topic, setTopic, format, setFormat, number, setNumber, isDisabled, setIsDisabled, setIsLoading, setReferences, addComment }) => {

  const chooseTopic = (event) => {
    if (!topic.trim()) {
      alert("Please enter a topic");
      return;
    }
    event.preventDefault();
    setIsDisabled(true);
    setIsLoading(true);

    taskService
        .submitUserInput({
          inputData: {
            comment: "",
          },
          objective: `Topic: ${topic}, citation format: ${format}, number of references: ${number}`
        })
        .then((returnedResponse) => {
          let parsed = taskService.parseAIResponse(returnedResponse.text);
          console.log(returnedResponse.text);
          const referencesBlock = parsed.references;
          const commentBlock = parsed.comment;
          if (referencesBlock) {
            let references = JSON.parse(referencesBlock);
            setReferences(references);
          }
          if (commentBlock) {
            addComment({ sender: "ai", comment: commentBlock });
          }
          setIsLoading(false);
        })
        .catch((error) => {
          console.log(error)
        });
  };

  return (
    <>
      <div className="topic-wrapper">
        <form onSubmit={chooseTopic} className="topic-input">
          <div className="input-label-container">
            <label for="topic"><h3>Topic</h3></label>
            <select
              id="topic"
              name="topic"
              type="text" 
              disabled={isDisabled}
              value={topic}
              onChange={(event) => setTopic(event.target.value)}
            >
              {constants.topics
                .map((topic, index) => ( 
                  <option key={index} value={topic}>{topic}</option>
              ))}
            </select>
          </div>
          <div className="input-label-container">
            <label for="format"><h3>Citation format</h3></label>
            <input 
              id="format"
              name="format"
              type="text" 
              disabled={isDisabled}
              placeholder="Citation format for the references"
              value={format}
              onChange={(event) => setFormat(event.target.value)}
            />
          </div>
          <div className="input-label-container">
            <label for="number"><h3>Number of<br/>references</h3></label>
            <input 
              id="number"
              name="number"
              type="number"
              min="1" 
              max="50" 
              disabled={isDisabled}
              value={number}
              onChange={(event) => setNumber(event.target.value)}
            />
          </div>
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

export default TopicForm;
