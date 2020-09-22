import { commitMutation, graphql } from "react-relay";
import environment from "../environment";
import { newCardMutation } from "./__generated__/newCardMutation.graphql";

import { ConnectionHandler } from 'relay-runtime';

const mutation = graphql`
  mutation newCardMutation(
    $author: String!
    ) {
    newCard(input: {author: $author}) {
      ok
      cardEdge {
        node {
          id
          author
          date
        }
      }
    }
  }
`;

// const configs: DeclarativeMutationConfig[] = [{
//   type: "RANGE_ADD",
//   edgeName: "edge",
//   parentID: "client:root",
//   connectionInfo: [{
//     key: 'App_allCards',
//     rangeBehavior: 'append',
//   }]
// }];


export function newCard(author: string) {
  const variables = { author };
  commitMutation<newCardMutation>(environment, {
    mutation,
    variables,
    // configs,
    updater: (store, data) => {
      const root = store.getRoot();
      const conn = ConnectionHandler.getConnection(root, "App_allCards");
      const payload = store.getRootField("newCard");

      // Get the edge of the newly created Todo record
      const newEdge = payload.getLinkedRecord('newCard');
      ConnectionHandler.insertEdgeAfter(conn!, newEdge!);
    },
    onCompleted: (res, err) => {
      console.log(res.newCard?.ok);
    },
    onError: (err) => console.error(err),
  });
}
