import taskService from '../services/task'

const MealDescriptionForm = ({ mealDescription, setMealDescription, isDisabled, setIsDisabled, setIsLoading, addMessage }) => {
  function parsePoetryAndComment(input) {
    // Initialize variables to store the parsed parts
    let poetryLine = "";
    let comment = "";
  
    // Trim the input to remove leading/trailing whitespace
    input = input.trim();
  
    // Check if the input starts with a '[' character
    if (input.startsWith('[')) {
        // Find the closing ']' character
        let endBracketIndex = input.indexOf(']');
        
        // If a closing ']' is found, extract the poetry line
        if (endBracketIndex !== -1) {
            poetryLine = input.substring(1, endBracketIndex).trim();
            // Extract the comment part if there is any text after the closing ']'
            if (endBracketIndex + 1 < input.length) {
                comment = input.substring(endBracketIndex + 1).trim();
            }
        }
    } else {
        // If the input doesn't start with '[', consider the whole input as a comment
        comment = input;
    }
  
    // console.log("Parsed: ", poetryLine, ", ", comment)
  
    return { poetryLine, comment };
  }
  
  function checkAndAddMessage(sender, text, comment, type) {
    text = (typeof text === 'string' && text.trim()) ? text : null;
    comment = (typeof comment === 'string' && comment.trim()) ? comment : null;
  
    if (text === null && comment === null) {
      console.log("no message");
    } else {
      addMessage({ sender: sender, text: text, comment: comment, type: "dialogue"}); 
    }
  }

  const setmealDescription = (event) => {
    if (!mealDescription.trim()) {
      alert("Please enter the description of your preferred meal plan");
      return;
    }
    event.preventDefault();
    setIsDisabled(true);
    setIsLoading(true);

    //Generate the first AI poem line after setting the meal description, it works based on how the prompt is set up
    taskService
      .submitUserInput({
        inputData: { 
        },
        text: "Recommend a weekly mealplan",
        objective: mealDescription
      })
      .then((returnedResponse) => {
        console.log(returnedResponse)
        setIsLoading(false)
      })
      .catch((error) => {
        console.log(error)
      });
  };

  return (
    <>
      <div className='meal-description-wrapper'>
        <form onSubmit={setmealDescription} className="meal-description-input">
          <label> <h3>Set your meal plan description</h3></label>
          <input 
            type="text" 
            disabled={isDisabled}
            placeholder="Tell me about your preffered food or meal"
            value={mealDescription}
            onChange={(event) => setMealDescription(event.target.value)}
          />
          <button 
            type="button"
            disabled={isDisabled}
            className="meal-description-submit-btn"
            onClick={setmealDescription}>
            Submit 
          </button>
        </form>
      </div>
    </>
  );
};

export default MealDescriptionForm;
