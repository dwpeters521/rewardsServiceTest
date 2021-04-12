export enum APIEndpointUrl {
  ADD_TRANSACTION = "add-transaction",
  SPEND_POINTS = "spend-points",
  GET_BALANCE = "get-balance",
}

interface IApiEndpoint {
  url: string;
  buttonName: string;
}

export const APIEndPoint: IApiEndpoint[] = [
  {
    url: APIEndpointUrl.ADD_TRANSACTION,
    buttonName: "Add Transaction",
  },
  {
    url: APIEndpointUrl.GET_BALANCE,
    buttonName: "Get Balance",
  },
  {
    url: APIEndpointUrl.SPEND_POINTS,
    buttonName: "Spend Points",
  },
];
