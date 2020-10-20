import React from 'react';
import { createPaginationContainer } from "react-relay";

function CardContainer(props) {
  return (
    <></>
  )
}

export default createPaginationContainer(CardContainer, {

}, {
  getVariables: ({ props, cursor }) => { return cursor };
})