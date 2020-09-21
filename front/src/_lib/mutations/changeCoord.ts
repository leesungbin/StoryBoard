import { commitMutation, graphql } from "react-relay";
import environment from "../environment";
import { changeCoordMutation } from "./__generated__/changeCoordMutation.graphql";

const mutation = graphql`
  mutation changeCoordMutation(
    $id: ID!
    $x: Int!
    $y: Int!
    ) {
    updateCard(input: {id: $id, x: $x, y: $y}) {
      ok
      card {
        x
        y
      }
    }
  }
`;
export function changeCoord(id: string, x: number, y: number) {
  const variables = { id, x, y };
  commitMutation<changeCoordMutation>(environment, {
    mutation,
    variables,
    onCompleted: (res, err) => {
      console.log(res.updateCard?.ok);
      console.log(res.updateCard?.card?.x, res.updateCard?.card?.y);
    },
    onError: (err) => console.error(err),
  });
}
