import axios from 'axios'

const baseUrl = "/api/v1/task"

const submitUserInput = (newUserMessage) => {
  const request = axios.post(`${baseUrl}/process`, newUserMessage)
  return request.then(response => response.data)
}

function parseAIResponse(input) {
  // Initialize variables to store the parsed parts
  let references = "";
  let comment = "";

  // Trim the input to remove leading/trailing whitespace
  input = input.trim();

  // Check if the input starts with a '[' character
  if (input.startsWith('[')) {
      // Find the closing ']' character
      let endBracketIndex = input.indexOf(']');
      
      // If a closing ']' is found, extract the references
      if (endBracketIndex !== -1) {
        references = input.substring(0, endBracketIndex + 1).trim();
          // Extract the comment part if there is any text after the closing ']'
          if (endBracketIndex + 2 < input.length) {
              comment = input.substring(endBracketIndex + 2).trim();
          }
      }
  } else {
      // If the input doesn't start with '[', consider the whole input as a comment
      comment = input;
  }
  return { references, comment };
}

const finishTask = (rating) => {
  const ratingjson = {
    metrics: {
      rating: rating, 
      task_name: "reference_list"
    }
  }
  axios
    .post(`${baseUrl}/finish`, ratingjson)
    .then((response) => {
      console.log(response)
    })
    .catch((error) => {
      console.log(error)
    })
}

export default { 
  finishTask,
  parseAIResponse,
  submitUserInput
}