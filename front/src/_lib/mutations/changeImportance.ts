import { commitMutation, graphql } from "react-relay";
import environment from "../environment";
import { changeImportanceMutation } from "./__generated__/changeImportanceMutation.graphql";

const mutation = graphql`
  mutation changeImportanceMutation(
    $id: ID!
    $importance: Int!
    ) {
    updateCard(input: {id: $id, importance: $importance}) {
      ok
      card {
        importance
      }
    }
  }
`;
export function changeImportance(id: string, importance: number) {
  const variables = { id, importance };
  return new Promise((resolve, reject) => {
    commitMutation<changeImportanceMutation>(environment, {
      mutation,
      variables,

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
