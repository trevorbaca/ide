import abjad
import ide


def test_Prompt___format___01():

    getter = ide.Getter()
    getter.append_string('value')
    prompt = getter.prompts[0]
    prompt_format = format(prompt)
    index = prompt_format.find('validation_function')
    modified_format = prompt_format[:index]
    modified_format = modified_format + ')'

    assert abjad.TestManager.compare(
        modified_format,
        r'''
        ide.Prompt(
            disallow_range=False,
            help_template='value must be string.',
            help_template_arguments=[],
            include_chevron=True,
            is_string=True,
            message='value',
            setup_statements=[],
            )
        '''
        )
