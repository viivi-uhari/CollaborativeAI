import constants from "../constants/constants";
import ModalWarning from "./ModalWarning";
import TextualWarning from "./TextualWarning";

const VisualWarning = ({ modalIsOpen, closeModal, currentWarning, setWarning }) => {

  function getRandomInt() {
    return Math.floor(Math.random() * 4);
  }

  function getWarningComponent() {
    let warning;
    if (!currentWarning) {
      warning = getRandomInt();
      setWarning(warning);
    } else {
      warning = currentWarning;
    }
    switch (warning) {
      case 0:
        return <TextualWarning text={constants.conciseWarning} />;
      case 1:
        return <TextualWarning text={constants.explanatoryWarning} />;
      case 2:
        return <ModalWarning text={constants.conciseWarning} modalIsOpen={modalIsOpen} closeModal={closeModal} />;
      case 3:
        return <ModalWarning text={constants.explanatoryWarning} modalIsOpen={modalIsOpen} closeModal={closeModal} />;
      default:
        return null;
    }
  }

  return getWarningComponent();

};

export default VisualWarning;
  