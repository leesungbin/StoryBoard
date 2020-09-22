import { commitMutation, graphql } from "react-relay";
import environment from "../environment";
// import { changeColorMutation } from "./__generated__/changeColorMutation.graphql";

const mutation = graphql`
  mutation changeColorMutation(
    $id: ID!
    $color: String!
    ) {
    updateCard(input: {id: $id, color: $color}) {
      ok
      card {
        color
      }
    }
  }
`;
export function changeColor(id: string, color: string) {
  const variables = { id, color };
  commitMutation(environment, {
    mutation,
    variables,
    onCompleted: (res, err) => {
    },
    optimisticUpdater: (store) => {
      const d = store.get(id);
      d?.setValue("color", color);
    },
    updater: (store) => {
      const d = store.get(id);
      d?.setValue("color", color);
    },
    onError: (err) => console.error(err),
  });
}
