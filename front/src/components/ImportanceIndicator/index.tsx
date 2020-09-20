import React from 'react';
import './indicator.scss';
import classNames from 'classnames';

type Props = {
  state: string,
  value: number,
  onClick?: () => void,
  onClickNumber?: () => void,
  onMouseEnter?: () => void,
  onMouseLeave?: () => void,
  onMouseEnterNumber?: () => void,
  onMouseLeaveNumber?: () => void,

}

export const ImportanceIndicator = (props: Props) => {
  return (
    <div className={classNames("main", props.state)} onClick={props.onClick}
      onMouseEnter={props.onMouseEnter} onMouseLeave={props.onMouseLeave}>
      <p onClick={props.onClickNumber}
        onMouseEnter={props.onMouseEnterNumber} onMouseLeave={props.onMouseLeaveNumber}>
        {props.value}
      </p>
    </div>
  )
}