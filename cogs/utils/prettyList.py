def int2Emoji(i):
    string = str(i)
    string = (string
              .replace('0', '0️⃣')
              .replace('1', '1️⃣')
              .replace('2', '2️⃣')
              .replace('3', '3️⃣')
              .replace('4', '4️⃣')
              .replace('5', '5️⃣')
              .replace('6', '6️⃣')
              .replace('7', '7️⃣')
              .replace('8', '8️⃣')
              .replace('9', '9️⃣'))

    return string


async def prettyList(ctx, title: str, rawList, units='', maxLength=5):
    repeat = min(maxLength, len(rawList))

    if maxLength == 0:
        repeat = len(rawList)

    if repeat < 1:
        await ctx.send("There is no result!")
        return

    output = [title]
    for i in range(repeat):
        if type(rawList[i]) == tuple:
            output.append(int2Emoji(i+1) +
                          f' {rawList[i][1]}: {rawList[i][0]} {units}')
        else:
            output.append(int2Emoji(i+1) + f' {rawList[i]}')

    await ctx.send('\n'.join(output))
