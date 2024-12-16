<template>
  <footer className="footer-container">
    <div className="acknowledge-section">
      <h2>Acknowledgement</h2>
      <br></br>
      <p>
        This work was funded by the European Union Horizon 2020 
        Research and Innovation Programme as part of the Humane-AI-net 
        project, under grant agreement number 952026. 
      </p> <br></br>
      <p>
        <strong>Humane-AI Net: </strong><a href="https://www.humane-ai.eu/" target="_blank">https://www.humane-ai.eu/</a>
      </p> <br></br>
      <p>
        <strong>AI Builder: </strong><a href="https://www.ai4europe.eu/ai-builder" target="_blank">https://www.ai4europe.eu/ai-builder</a>
      </p>
    </div>
    <div className="logo-section">
      <img src="../assets/image1.png" alt="Project Logo" />
    </div>
  </footer>
</template>

<script>
export default {
  name: "Footer"
}
</script>

<style scoped>
.footer-container {
  background-color: rgb(76, 70, 163);
  color: white;
  padding: 50px;
  display: flex;
  justify-content: space-between
}

.footer-container h2,
.footer-container p {
  margin-bottom: 10px;
}

.footer-container img {
  max-width: 100%;
  height: auto;
}

.footer-container h2 {
  font-size: 20px;
}

.acknowledge-section{
  flex: 1;
  max-width: 600px;
  margin-right: 20px;
  padding-right: 20px;
}

.logo-section img {
  width: 600px; 
}
a:link {
  color: white;
  background-color: transparent;
  text-decoration: none;
}

a:visited {
  color: white;
  background-color: transparent;
  text-decoration: none;
}

a:hover {
  color: red;
  background-color: transparent;
  text-decoration: underline;
}

a:active {
  color: yellow;
  background-color: transparent;
  text-decoration: underline;
}
</style>