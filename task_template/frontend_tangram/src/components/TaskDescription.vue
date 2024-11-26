<template>
  <div>
    <h2>🧩 Tangram task</h2>
      <h3>📜 Rules</h3>
      <ol>
        <li>Give an objective (a shape such as a car or a house) for the tangram to the AI</li>
        <li>The current tangram game version supports only two pieces: a triangle and a square (We will add more in the future)</li>
        <li>You and AI take turns to solve the tangram based on the objective. You go first</li>
        <li>To do your turn, move and adjust a piece of tangram and submit it alongside your message in the chat box. Then, the AI will give the next instruction</li>
        <li><strong>Basic control:  </strong>right click to rotate, ctrl + left click to flip the tangram piece</li>
        <li>Quick guide coming soon!</li>
      </ol>
  </div>
</template>

<script>
export default {
  name: "TaskDescription"
}
</script>