import { defineStore } from 'pinia'
import axios from 'axios'
import type { Task, TaskInteraction, TaskSubmission } from './types'

const taskField = 'CollaborativeAI:Task'
const interactionField = 'CollaborativeAI:Interaction'

export const useTaskStore = defineStore({
  id: 'tasks',
  state: () => ({
    tasks: [] as Task[],
    selectedTask: (sessionStorage.getItem(taskField)
      ? JSON.parse(sessionStorage.getItem(taskField) as string)
      : {}) as Task,
    currentInteraction: (sessionStorage.getItem(interactionField)
      ? JSON.parse(sessionStorage.getItem(interactionField) as string)
      : {}) as TaskInteraction, // Maybe we can define this type later, but it is likely to be quite specific per task...
    lastInteraction: {} as any
  }),
  actions: {
    updateTasks() {
      // TODO: Replace this with a real API call
      this.tasks = [
        {
          id: 'tangram',
          title: 'Tangram design Task',
          needsText: false,
          description: `The objective of this task is to use a tangram game to collaboratively fullfil a task together with an AI. 
                        The player and the AI take turns in placing (or moving) pieces of a tangram game. 
                        Please define what task you and the AI will be working on.`
        },
        {
          id: 'tangram2',
          title: 'Tangram design Task 2',
          needsText: true,
          description: `The objective of this task is to use a tangram game to collaboratively fullfil a task together with an AI. 
                        The player and the AI take turns in placing (or moving) pieces of a tangram game. 
                        Each player should motivate what their turn does (in writing).
                        Please define what task you and the AI will be working on.`
        }
      ]
    },
    getSelectedTask() {
      return this.selectedTask
    },
    /**
     * Select a task from the list of tasks
     * @param task
     */
    selectTask(task: Task) {
      this.selectedTask = task
      sessionStorage.setItem(taskField, JSON.stringify(task))
      this.currentInteraction = {
        task: task,
        objective: '',
        interactionData: {},
        isLoading: false,
        history: [],
        submissionHistory: []
      }
      this.storeInteraction()
      console.log('Task selected: ', task)
    },
    /**
     * Set the objective of the current interaction
     */
    setObjective(objective: string) {
      this.currentInteraction.objective = objective
      this.storeInteraction()
    },
    /**
     * Stores the current Interaction in the store
     */
    storeInteraction() {
      sessionStorage.setItem(interactionField, JSON.stringify(this.currentInteraction))
    },
    /**
     * Submit user input to the backend.
     * This triggers the currentInteraction to go into a isLoading stage
     * The data submitted is task specific and
     * @param data
     */
    submitUserInput(data: TaskSubmission) {
      this.currentInteraction.isLoading = true
      if (this.selectedTask) {
        console.log('Pushing to history')
        console.log(data)
        data.displayData.handled = true
        this.currentInteraction.history.push(data.displayData)
        this.currentInteraction.submissionHistory.push(data.submission)
        this.storeInteraction()

        /*        const responseData = { data: { tangram: '{"Big Triangle 1" : ["(723,140)", 45]}' } }
            const AISubmission = {
              role: 'AI',
              data: responseData.data
            }
            this.currentInteraction.submissionHistory.push(AISubmission)
            this.lastInteraction = AISubmission
            sessionStorage.setItem(interactionField, JSON.stringify(this.currentInteraction))
            this.currentInteraction.isLoading = false
*/
        axios
          .post(`/api/v1/task/process`, {
            inputData: data.submission.data.tangramData,
            image: data.submission.data.image,
            objective: this.currentInteraction.objective
          })
          .then((response) => {
            // Handle response
            console.log(response)
            const responseData = response.data
            const submissiondata = { tangram: responseData.text }
            const AISubmission = {
              role: 'AI',
              data: submissiondata
            }
            this.currentInteraction.submissionHistory.push(AISubmission)
            this.lastInteraction = AISubmission
            sessionStorage.setItem(interactionField, JSON.stringify(this.currentInteraction))
            this.currentInteraction.isLoading = false
          }) // Commented out for now, as we don't have a backend yet */
      }
    },
    /**
     * Finish the task, resetting history and everything.
     */
    finishTask(rating: any) {
      const ratingjson = { metrics: rating }
      axios.post(`/api/v1/task/finish`, ratingjson).then((response) => {
        // successfully submitted data.
        this.selectedTask = {} as Task
        this.currentInteraction = {} as TaskInteraction
        sessionStorage.removeItem(taskField)
        sessionStorage.removeItem(interactionField)
        this.lastInteraction = {}
      })
    }
  }
})
