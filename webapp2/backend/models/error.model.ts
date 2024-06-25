type ErrorCodes = 400 | 401 | 403 | 404 | 500;

export class BackendError extends Error {
  code: ErrorCodes;
  message: string;
  error: Error | undefined;

  constructor(code: ErrorCodes, message: string, error: Error | undefined) {
    super();

    this.code = code;
    this.message = message;
    this.error = error;
  }
}

export class ServiceError extends BackendError {
  constructor(message: string, error: Error) {
    super(500, message, error);
  }
}

export class NotFoundError extends BackendError {
  constructor(message: string) {
    super(404, message, undefined);
  }
}

export class UserError extends BackendError {
  constructor(message: string) {
    super(400, message, undefined);
  }
}
