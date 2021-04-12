import { useState } from "react";
import { transformErrors } from "../shared/transformErrors";
import axios from "axios";
import { APIEndpointUrl } from "../../APIEndpoint";

export interface Inputs {
  points: number;
}

interface IResponseState {
  results: ISpendPointsResult[];
  errors: string[];
}

export interface ISpendPointsPayload {
  points: number;
}

export interface ISpendPointsResult {
  payer: string;
  points: string;
}

export interface ISpendPointsData {
  results: ISpendPointsResult[];
  success: boolean;
  code: number;
}

export interface ISpendPointsResponse {
  data: ISpendPointsData;
  status: number;
  error?: {
    message: string;
  };
}

export async function spendPoints(
  payload: ISpendPointsPayload
): Promise<ISpendPointsResponse> {
  return await axios.post(`${APIEndpointUrl.SPEND_POINTS}/`, payload);
}

export function useSpendPoints() {
  const [{ results, errors }, setResponse] = useState<IResponseState>({
    results: [],
    errors: [],
  });

  const onSubmit = async (data: Inputs) => {
    try {
      const res: ISpendPointsResponse = await spendPoints(data);
      setResponse({ results: res.data.results, errors: [] });
    } catch (error) {
      const transformedErrors = transformErrors(error.response.data.errors);
      setResponse({ results: [], errors: transformedErrors });
    }
  };

  return {
    operations: {
      onSubmit,
    },
    models: {
      results,
      errors,
    },
  };
}
