import React from 'react';
import './icon.scss';
import check from '../../assets/check.png';
import edit from '../../assets/edit.png';
import palette from '../../assets/palette.png';
import deleteicon from '../../assets/deleteicon.png';
import plus from '../../assets/plus.png';

type Props = {
  name: string,
  onClick?: () => void,
}
export const Icon = ({ name, onClick }: Props) => {
  switch (name) {
    case "check":
      return <img className="icon" src={check} alt="check" onClick={onClick} />
    case "edit":
      return <img className="icon" src={edit} alt="edit" onClick={onClick} />
    case "delete":
      return <img className="icon" src={deleteicon} alt="delete" onClick={onClick} />
    case "palette":
      return <img className="icon" src={palette} alt="palette" onClick={onClick} />
    case "plus":
      return <img className="icon_big" src={plus} alt="plus" onClick={onClick} />
  }
  return <></>
}
