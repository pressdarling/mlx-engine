from typing import NamedTuple

import mlx.core as mx


class TokenLogprob(NamedTuple):
    id: int
    text: str
    logprob: float


def summarize_top_logprobs(
    tokenizer, logprobs: mx.array, top_logprobs: int
) -> list[TokenLogprob]:
    # find the sorted indices (in descending order) of the logprobs
    sorted_indices = mx.argsort(-logprobs)

    # sort the logprobs in descending order
    sorted_logprobs = logprobs[..., sorted_indices]

    # slice the top logprobs
    top_indices = sorted_indices[:top_logprobs]
    top_logprobs = sorted_logprobs[:top_logprobs]

    # decode the top indices
    text_list = [tokenizer.decode(index) for index in top_indices.tolist()]

    # return list of TokenLogprob with id (int), text (str), and logprob (float)
    return [
        TokenLogprob(int(idx), txt, float(prob))
        for idx, txt, prob in zip(
            top_indices.tolist(), text_list, top_logprobs.tolist()
        )
    ]
