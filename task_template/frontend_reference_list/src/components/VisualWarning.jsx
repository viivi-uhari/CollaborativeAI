import { explanatoryWarning } from "../utils/config";
import ModalWarning from "./ModalWarning";
import TextualWarning from "./TextualWarning";

const VisualWarning = ({ warningModalIsOpen, closeWarningModal, participantId }) => {
  const getWarningComponent = () => {
    const remainder = participantId % 3;
    console.log(remainder);
    switch (remainder) {
      case 0:
        return <TextualWarning text={explanatoryWarning} />;
      case 1:
        return <ModalWarning text={explanatoryWarning} warningModalIsOpen={warningModalIsOpen} closeWarningModal={closeWarningModal} />;
      case 2:
        return <div/>; // No warning = control
      default:
        return null;
    }
  }
  return getWarningComponent();
};

export default VisualWarning;
  