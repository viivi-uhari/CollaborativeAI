import axios from 'axios'

const baseUrl = "/api/v1/task"

const finishTask = (rating) => {
  const ratingjson = {
    metrics: {
      rating: rating, 
      task_name: "poetry_task" //change this to your task name
    }
  }
  console.log(ratingjson)
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
  finishTask
}