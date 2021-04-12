import { useEffect, useState } from "react";
import axios from "axios";
import { APIEndpointUrl } from "../../APIEndpoint";

interface IResultState {
  payer: string;
  points: number;
}

interface IResponseState {
  results: IResultState[];
  loading: boolean;
}

interface IGetBalanceResult {
  [payer: string]: number;
}

interface IGetBalanceData {
  results: IGetBalanceResult;
}

interface IGetBalanceResponse {
  data: IGetBalanceData;
  status: number;
}

export async function getBalance(): Promise<IGetBalanceResponse> {
  return await axios.get(`${APIEndpointUrl.GET_BALANCE}/`);
}

function transformBalance(
  balanceResponse: IGetBalanceResponse
): IResultState[] {
  const transformedBalance = [];
  const {
    data: { results },
  } = balanceResponse;
  for (let key in results) {
    transformedBalance.push({
      payer: key,
      points: results[key],
    });
  }

  return transformedBalance;
}

export function useFetchBalance() {
  const [{ results, loading }, setResponse] = useState<IResponseState>({
    results: [],
    loading: true,
  });
  useEffect(() => {
    getBalance().then((response) => {
      const transformedResponse = transformBalance(response);

      setResponse({ results: transformedResponse, loading: false });
    });
  }, []);

  return {
    models: {
      results,
      loading,
    },
  };
}
