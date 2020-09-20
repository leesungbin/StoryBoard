import React, { useState } from 'react';
import { createFragmentContainer, graphql, RelayProp } from "react-relay";
import { Card_card } from "./__generated__/Card_card.graphql";
import './card.scss';
import classNames from 'classnames';
import moment from 'moment';
import 'moment/locale/ko';
import { ImportanceIndicator } from "../ImportanceIndicator";
import Draggable from 'react-draggable';
import { Icon } from "./Icon";
import { changeCoord } from "../../_lib/mutations/changeCoord";

type Props = {
  relay: RelayProp,
  card: Card_card | null,
}


moment.locale('ko');

const Card = (props: Props) => {
  const { card } = props;
  const [isSelected, setSelected] = useState<Boolean>(false);
  const [isOnIndicator, toggleIndicator] = useState<Boolean>(false);
  const [isOnIndicatorNumber, toggleIndicatorNumber] = useState<Boolean>(false);
  const cardState = ["will", "now", "fin", "meet"];
  const [procedingState, setPs] = useState<string | undefined>(card?.state);
  const [importance, setImportance] = useState<number | undefined>(card?.importance);

  const date = moment(card?.date as string).fromNow();


  return card &&
    <Draggable handle=".handler" defaultPosition={{ x: card.x, y: card.y }}
      onStop={(_, data) => { changeCoord(card.id, data.x, data.y); console.log(data.x, data.y); }}
    >
      <div className={classNames("card", card.color, { "selected": isSelected })}>
        <div className="handler"
          onMouseDownCapture={() => !isOnIndicator && setSelected(true)}
          onMouseUpCapture={() => !isOnIndicator && setSelected(false)}
        >
          <div className="grab" />
        </div>
        <div className="sub">
          <div className="top">
            <h1>{card.title}</h1>
            <div>{newLineParser(card.content)}</div>
          </div>
          <div className="bot">
            <div>
              <p>by {card.author} - {date}</p>
              <Icon name="delete" />
              <Icon name="palette" />
            </div>
            {procedingState && typeof (importance) === 'number' && <ImportanceIndicator state={procedingState} value={importance}
              onClick={() => { !isOnIndicatorNumber && setPs(cardState[(cardState.indexOf(procedingState) + 1) % cardState.length]) }}
              onMouseEnter={() => { toggleIndicator(true) }}
              onMouseLeave={() => { toggleIndicator(false) }}
              onClickNumber={() => setImportance((importance + 1) % 4)}
              onMouseEnterNumber={() => { toggleIndicatorNumber(true) }}
              onMouseLeaveNumber={() => { toggleIndicatorNumber(false) }}
            />
            }
          </div>
        </div>
      </div >
    </Draggable>
};
const newLineParser = (text: string | null) => {
  return text && text.split("\n").map((e, i) => <p key={i}>{e}</p>);
}

export default createFragmentContainer(Card, {
  card: graphql`
    fragment Card_card on CardNode {
        id
      title
      content
      author
      date
      state
      importance
      color
      x
      y
    }
  `
})