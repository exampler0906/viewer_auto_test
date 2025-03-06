import clang.cindex
index = clang.cindex.Index.create()
tu = index.parse('test.cpp')
for node in tu.cursor.get_children():
    if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        print(node.extent.start.line, node.extent.end.line)