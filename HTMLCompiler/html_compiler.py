"""
HTML Compiler
"""

import markdown
import yaml

STARTING_COMMENT = "<!-- This is an auto-generated file. Edit it if you want, I don't care -->\n"
MAGIC_REPL_TAG = "<GENERATE></GENERATE>"

class HTMLCompiler:

    def __init__(self, config_file):
        """
        Create HTML compiler instance

        Args:
        config_file -- YAML configuration file path
        """

        self.config_file = config_file


    def compile_all(self):
        """
        Build output
        """

        # Open config
        with open(self.config_file, 'r') as yaml_file:
            config_data = yaml.safe_load(yaml_file)

        # Compile each output file seperately
        for key in config_data:
            print("Compiling " + key + "!")
            all_data = STARTING_COMMENT

            # Open template
            with open(config_data[key]['template']['source'], 'r') as template_file:
                template_data = template_file.read()

                # Update template with fill-in params
                for repl_content in config_data[key]['template']['replace_content']:
                    template_data = template_data.replace(repl_content, config_data[key]['template']['replace_content'][repl_content])

            all_data += template_data

            # Parse source file
            with open(config_data[key]['content']['source'], 'r') as source_file:
                source_data = source_file.read()
                md_source_data = markdown.markdown(source_data)

                # Update converted markdown
                for repl_content in config_data[key]['content']['replace_content']:
                    md_source_data = md_source_data.replace(repl_content, config_data[key]['content']['replace_content'][repl_content])

            # Merge template and generated HTML
            # Use magic tag for this
            # TODO: Maybe don't use a magic tag?
            all_data = all_data.replace(MAGIC_REPL_TAG, md_source_data)

            # Save file
            with open(config_data[key]['out_file'], 'w') as dest_file:
                dest_file.write(all_data)
                dest_file.close()