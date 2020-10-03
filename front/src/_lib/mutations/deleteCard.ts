import { commitMutation, DeclarativeMutationConfig, graphql } from "react-relay";
import environment from "../environment";
import { deleteCardMutation } from "./__generated__/deleteCardMutation.graphql";

const mutation = graphql`
  mutation deleteCardMutation(
    $id: ID!
    ) {
    deleteCard(input: {id: $id}) {
      ok
      id
    }
  }
`;

const configs: DeclarativeMutationConfig[] = [{
  type: 'RANGE_DELETE',
  deletedIDFieldName: "id",
  parentID: "client:root",
  connectionKeys: [{
    key: "App_allCards",
  }],
  pathToConnection: ["edges", "allCards"],
}];

export function deleteCard(id: string) {
  const variables = { id };
  return new Promise((resolve, reject) => commitMutation<deleteCardMutation>(environment, {
    mutation,
    variables,
    configs,
    optimisticUpdater: (store) => {
      store.delete(id);
    },
    // updater: (store, data) => {
    //   store.delete(id);
    // },
    onCompleted: (res, err) => {
      console.log(res.deleteCard);
      resolve();
    },
    onError: (err) => { console.error(err); reject() }
  }))

}
