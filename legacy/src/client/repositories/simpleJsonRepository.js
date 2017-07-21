// @flow

class simpleJsonRepository {
  static get(url): Promise {
    return new Promise((resolve, reject) =>
      $.ajax({
        dataType: 'json',
        url,
        cache: false,
      })
      .fail((jqXHR, textStatus, error) =>
        reject(
          {
            jqXHR,
            textStatus,
            error,
          },
        ),
      )
      .done(data =>
        resolve(
          data,
        ),
      ),
    );
  }
}

export default simpleJsonRepository;
