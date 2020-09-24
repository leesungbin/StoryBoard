import { commitMutation, graphql } from "react-relay";
import environment from "../environment";
import { newCardMutation } from "./__generated__/newCardMutation.graphql";

import { DeclarativeMutationConfig } from 'relay-runtime';

const mutation = graphql`
  mutation newCardMutation(
    $author: String!
    ) {
    newCard(input: {author: $author}) {
      ok
      cardEdge {
        cursor
        node {
          id
          author
          color
          state
          date
          x
          y
        }
      }
    }
  }
`;

const configs: DeclarativeMutationConfig[] = [{
  type: "RANGE_ADD",
  edgeName: "cardEdge",
  parentID: "client:root",
  connectionInfo: [{
    key: 'App_allCards',
    rangeBehavior: 'append',
  }]
}];


export function newCard(author: string) {
  const variables = { author };
  return new Promise((resolve, reject) => {
    commitMutation<newCardMutation>(environment, {
      mutation,
      variables,
      configs,
      onCompleted: (res, err) => {
        resolve();
      },
      onError: (err) => {
        console.error(err);
        reject();
      }
    });
  })
}
