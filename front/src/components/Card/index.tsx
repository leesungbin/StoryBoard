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
import { deleteCard } from "../../_lib/mutations/deleteCard";
import { changeColor } from "../../_lib/mutations/changeColor";
import { changeImportance } from "../../_lib/mutations/changeImportance";
import { changeState } from "../../_lib/mutations/changeState";

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
  const [importance, setImportance] = useState<number | undefined>(card?.importance);
  const cardColor = ["blue", "red", "yellow", "green"];

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
              <Icon name="delete" onClick={() => deleteCard(card.id)} />
              <Icon name="palette" onClick={() => changeColor(card.id, cardColor[(cardColor.indexOf(card.color) + 1) % cardColor.length])} />
            </div>
            {typeof (importance) === 'number' && <ImportanceIndicator state={card.state} value={importance}
              onClick={() => {
                !isOnIndicatorNumber &&
                  changeState(card.id, cardState[(cardState.indexOf(card.state) + 1) % cardState.length])
              }}
              onMouseEnter={() => { toggleIndicator(true) }}
              onMouseLeave={() => { toggleIndicator(false) }}
              onClickNumber={() => { setImportance((importance + 1) % 4); changeImportance(card.id, (importance + 1) % 4); }}
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