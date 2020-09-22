import { commitMutation, graphql } from "react-relay";
import environment from "../environment";
import { changeStateMutation } from "./__generated__/changeStateMutation.graphql";

const mutation = graphql`
  mutation changeStateMutation(
    $id: ID!
    $state: String!
    ) {
    updateCard(input: {id: $id, state: $state}) {
      ok
      card {
        state
      }
    }
  }
`;
export function changeState(id: string, state: string) {
  const variables = { id, state };
  return new Promise((resolve, reject) => {
    commitMutation<changeStateMutation>(environment, {
      mutation,
      variables,
      onCompleted: (res, err) => {
        resolve();
      },
      optimisticUpdater: (store) => {
        const d = store.get(id);
        d?.setValue("state", state);
      },
      updater: (store) => {
        const d = store.get(id);
        d?.setValue("state", state);
      },
      onError: (err) => {
        console.error(err);
        reject();
      }
    });
  })

}
