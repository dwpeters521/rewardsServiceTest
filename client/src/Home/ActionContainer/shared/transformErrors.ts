export interface IErrorsResponse {
  [field: string]: string[];
}

export function transformErrors(errorsResponse: IErrorsResponse): string[] {
  const errors = [];

  for (let field in errorsResponse) {
    const fieldErrors = errorsResponse[field];
    for (let error of fieldErrors) {
      errors.push(`${error} For ${field.toUpperCase()}`);
    }
  }

  return errors;
}
