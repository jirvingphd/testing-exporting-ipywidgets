def ihelp(function_or_mod, show_help=True, show_code=True,return_code=False,colab=False,file_location=False): 
    """Call on any module or functon to display the object's
    help command printout AND/OR soruce code displayed as Markdown
    using Python-syntax"""

    import inspect
    from IPython.display import display, Markdown
    page_header = '---'*28
    footer = '---'*28+'\n'
    if show_help:
        print(page_header)
        banner = ''.join(["---"*2,' HELP ',"---"*24,'\n'])
        print(banner)
        help(function_or_mod)
        # print(footer)
        
    if show_code:
        print(page_header)

        banner = ''.join(["---"*2,' SOURCE -',"---"*23])
        print(banner)
        try:
            import inspect
            source_DF = inspect.getsource(function_or_mod)            

            if colab == False:
                # display(Markdown(f'___\n'))
                output = "```python" +'\n'+source_DF+'\n'+"```"
                # print(source_DF)    
                display(Markdown(output))
            else:

                print(banner)
                print(source_DF)

        except TypeError:
            pass
            # display(Markdown)
            
    
    if file_location:
        file_loc = inspect.getfile(function_or_mod)
        banner = ''.join(["---"*2,' FILE LOCATION ',"---"*21])
        print(page_header)
        print(banner)
        print(file_loc)

    # print(footer)

    if return_code:
        return source_DF


def ihelp_menu2(function_list, json_file='ihelp_output.txt',to_embed=False):
    """Accepts a list of string names for loaded modules/functions to save the `help` output and 
    inspect.getsource() outputs to dictionary for later reference and display"""
    ## One way using sys to write txt file
    import pandas as pd
    import sys
    import inspect
    from io import StringIO
    notebook_output = sys.stdout
    result = StringIO()
    sys.stdout=result
    
    ## Turn single input into a list
    if isinstance(function_list,list)==False:
        function_list = [function_list]
    
    ## Make a dictionary of{function_name : function_object}
    functions_dict = dict()
    for fun in function_list:
        
        ## if input is a string, save string as key, and eval(function) as value
        if isinstance(fun, str):
            functions_dict[fun] = eval(fun)

        ## if input is a function, get the name of function using inspect and make key, function as value
        elif inspect.isfunction(fun):

            members= inspect.getmembers(fun)
            member_df = pd.DataFrame(members,columns=['param','values']).set_index('param')

            fun_name = member_df.loc['__name__'].values[0]
            functions_dict[fun_name] = fun
            
            
    ## Create an output dict to store results for functions
    output_dict = {}

    for fun_name, real_func in functions_dict.items():
        
        output_dict[fun_name] = {}
                
        ## First save help
        help(real_func)
        output_dict[fun_name]['help'] = result.getvalue()
        
        ## Clear contents of io stream
        result.truncate(0)
        
        try:
            ## Next save source
            print(inspect.getsource(real_func)) #eval(fun)))###f"{eval(fun)}"))
        except:
            print("Source code for object was not found")
        output_dict[fun_name]['source'] = result.getvalue()
        
        ## clear contents of io stream
        result.truncate(0)
        
        
        ## Get file location
        try:
            file_loc = inspect.getfile(real_func)
            print(file_loc)
        except:
            print("File location not found")
            
        output_dict[fun_name]['file_location'] =result.getvalue()
        
        
        ## clear contents of io stream
        result.truncate(0)        
                
        
    ## Reset display back to notebook
    sys.stdout = notebook_output    

    
    with open(json_file,'w') as f:
        import json
        json.dump(output_dict,f)

    
    ## CREATE INTERACTIVE MENU
    from ipywidgets import interact, interactive, interactive_output
    import ipywidgets as widgets
    from IPython.display import display


    ## Check boxes
    check_help = widgets.Checkbox(description="Show 'help(func)'",value=True)
    check_source = widgets.Checkbox(description="Show source code",value=True)
    check_fileloc=widgets.Checkbox(description="Show source filepath",value=False)
    check_boxes = widgets.HBox(children=[check_help,check_source,check_fileloc])

    ## dropdown menu (dropdown, label, button)
    dropdown = widgets.Dropdown(options=list(output_dict.keys()))
    label = widgets.Label('Function Menu')
    button = widgets.ToggleButton(description='Show/hide',value=False)
    
    ## Putting it all together
    title = widgets.Label('iHelp Menu: View Help and/or Source Code')
    menu = widgets.HBox(children=[label,dropdown,button])
    titled_menu = widgets.VBox(children=[title,menu])
    full_layout = widgets.GridBox(children=[titled_menu,check_boxes],box_style='warning')
    
    
    
    ## Define output manager
    # show_output = widgets.Output()

    def dropdown_event(change): 
        new_key = change.new
        output_display = output_dict[new_key]
    dropdown.observe(dropdown_event,names='values')

    
    def show_ihelp(display_help=button.value,function=dropdown.value,
                   show_help=check_help.value,show_code=check_source.value, show_file=check_fileloc.value):#,
                   #ouput_dict=output_dict):

        from IPython.display import Markdown
#         import functions_combined_BEST as ji
        from IPython.display import display        
        page_header = '---'*28
        import json
        with open(json_file,'r') as f:
            output_dict = json.load(f)
        
        
        func_dict = output_dict[function]

        if display_help:
            if show_help:
#                 display(print(func_dict['help']))
                print(page_header)
                banner = ''.join(["---"*2,' HELP ',"---"*24,'\n'])
                print(banner)
                print(func_dict['help'])

            if show_code:
                print(page_header)

                banner = ''.join(["---"*2,' SOURCE -',"---"*23])
                print(banner)
                source_code = "```python\n"
                source_code += func_dict['source']
                source_code += "```"
                display(Markdown(source_code))
            
            
            if show_file:
                print(page_header)
                banner = ''.join(["---"*2,' FILE LOCATION ',"---"*21])
                print(banner)
                
                file_loc = func_dict['file_location']
                print(file_loc)
                
            if show_help==False & show_code==False & show_file==False:
                display('Check at least one "Show" checkbox for output.')
                
        else:
            display('Press "Show/hide" for display')
            
    ## Fully integrated output
    output = widgets.interactive_output(show_ihelp,{'display_help':button,
                                                   'function':dropdown,
                                                   'show_help':check_help,
                                                   'show_code':check_source,
                                                   'show_file':check_fileloc})

    if to_embed:
        return full_layout, output
    else:
        display(full_layout, output)
