import { conciseWarning, explanatoryWarning } from "../utils/config";
import ModalWarning from "./ModalWarning";
import TextualWarning from "./TextualWarning";

const VisualWarning = ({ modalIsOpen, closeModal, currentWarning, setWarning }) => {

  const getRandomInt = () => {
    return Math.floor(Math.random() * 4);
  }

  const getWarningComponent = () => {
    let warning;
    if (!currentWarning) {
      warning = getRandomInt();
      setWarning(warning);
    } else {
      warning = currentWarning;
    }
    switch (warning) {
      case 0:
        return <TextualWarning text={conciseWarning} />;
      case 1:
        return <TextualWarning text={explanatoryWarning} />;
      case 2:
        return <ModalWarning text={conciseWarning} modalIsOpen={modalIsOpen} closeModal={closeModal} />;
      case 3:
        return <ModalWarning text={explanatoryWarning} modalIsOpen={modalIsOpen} closeModal={closeModal} />;
      default:
        return null;
    }
  }
  return getWarningComponent();
};

export default VisualWarning;
  