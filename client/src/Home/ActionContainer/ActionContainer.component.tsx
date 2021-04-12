import React from "react";
import { APIEndpointUrl } from "../APIEndpoint";
import AddTransactionForm from "./AddTransactionForm/AddTransactionForm.component";
import BalanceTable from "./BalanceTable/BalanceTable.component";
import SpendPointsForm from "./SpendPointsForm/SpendPointsForm.component";

interface IFormProps {
  APIUrl: string;
}

export default function ActionContainer({ APIUrl }: IFormProps) {
  if (APIUrl === APIEndpointUrl.ADD_TRANSACTION) {
    return <AddTransactionForm />;
  } else if (APIUrl === APIEndpointUrl.SPEND_POINTS) {
    return <SpendPointsForm />;
  } else if (APIUrl === APIEndpointUrl.GET_BALANCE) {
    return <BalanceTable />;
  } else {
    return null;
  }
}
