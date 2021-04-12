import { useState } from "react";
import { transformErrors } from "../shared/transformErrors";
import axios from "axios";
import { APIEndpointUrl } from "../../APIEndpoint";

export interface Inputs {
  payer: string;
  points: string;
}

export interface IAddTransactionPayload {
  payer: string;
  points: string;
}

export async function addTransaction(payload: IAddTransactionPayload) {
  return await axios.post(`${APIEndpointUrl.ADD_TRANSACTION}/`, payload);
}

export function useAddTransaction() {
  const [addedTransaction, setAddedTransaction] = useState<boolean>(false);
  const [errors, setErrors] = useState<string[]>([]);
  const onSubmit = async (data: Inputs) => {
    const payload = {
      ...data,
      timestamp: new Date(),
    };

    try {
      await addTransaction(payload);

      setAddedTransaction(true);
      setErrors([]);
    } catch (error) {
      const transformedErrors: string[] = transformErrors(
        error.response.data.errors
      );
      setErrors(transformedErrors);
    }
  };

  return {
    operations: {
      onSubmit,
    },
    models: {
      addedTransaction,
      errors,
    },
  };
}
