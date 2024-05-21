export type Task = {
  id: string
  title: string
  needsText: boolean
  description: string
}

export type TaskInteraction = {
  task: Task
  objective: string
  interactionData: any
  isLoading: boolean
  history: Array<DisplayMessage>
  submissionHistory: Array<SubmissionObject>
}

export type DisplayMessage = {
  message: string
  containsImage: boolean
  imageURL: string
  role: string
  handled: boolean
}

export type SubmissionObject = {
  role: string
  poemText: string
  commentText: string
}

export type TaskSubmission = {
  submission: SubmissionObject
  displayData: DisplayMessage
}
